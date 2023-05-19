#ifndef _FLEXFLOW_RUNTIME_SRC_EXECUTABLE_TASK_INVOCATION_H
#define _FLEXFLOW_RUNTIME_SRC_EXECUTABLE_TASK_INVOCATION_H

#include "task_invocation.h"

namespace FlexFlow {

using ExecutableArgSpec = variant<ConcreteArgSpec, IndexArgSpec, CheckedTypedFuture, CheckedTypedFutureMap, TaskInvocationSpec>;
using NonvariadicExecutableTensorSpec = parallel_tensor_guid_t;
using VariadicExecutableTensorSpec = std::vector<parallel_tensor_guid_t>;
using ExecutableTensorSpec = variant<NonvariadicExecutableTensorSpec, VariadicExecutableTensorSpec>;

bool is_variadic(ExecutableTensorSpec const &);
bool is_nonvariadic(ExecutableTensorSpec const &);
NonvariadicExecutableTensorSpec get_nonvariadic(ExecutableTensorSpec const &);
VariadicExecutableTensorSpec get_variadic(ExecutableTensorSpec const &);

struct ExecutableTaskBinding {
public:
  InvocationType invocation_type;
  std::unordered_map<slot_id, ExecutableArgSpec> arg_bindings;
  std::unordered_map<slot_id, ExecutableTensorSpec> tensor_bindings;
  optional<NonvariadicExecutableTensorSpec> domain_spec = nullopt;
};

bool is_variadic(ExecutableTaskBinding const &, slot_id);
bool is_nonvariadic(ExecutableTaskBinding const &, slot_id);

struct ExecutableTaskInvocation : public use_visitable_cmp<ExecutableTaskInvocation> {
public:
  ExecutableTaskInvocation() = delete;
  ExecutableTaskInvocation(task_id_t const &task_id, TaskBinding const &binding);

public:
  task_id_t task_id;
  ExecutableTaskBinding binding;
};


TaskReturnAccessor execute_task(LegionConfig const &config, 
                                TaskInvocation const &,
                                RuntimeBacking const &backing);


}

#endif
